/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: santony
 *
 * Created on December 8, 2018, 6:47 PM
 */

#include <cstdlib>
#include <iostream>
#include <poppler-document.h>
#include <poppler-image.h>
#include <poppler-page.h>
#include <poppler-page-renderer.h>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <sstream>
#include <unistd.h>
#include <stdlib.h>
#include <sys/inotify.h>
#include <signal.h>
#include <sys/stat.h>
#include <algorithm>
#include <errno.h>
#include <poll.h>
#include <map>
#include <ftw.h>
#include <mutex>
#include <thread>
#include <condition_variable>
#include <atomic>
#include <fstream>
#include <future>

#define WITHTHREADPOOL

#ifdef WITHTHREADPOOL            
#include "ThreadPool.h"
#endif
using namespace std;
using namespace tesseract;
using namespace poppler;

#define MAX_DESCR       1024
#define MAX_EVENTS      1024
#define FILE_NAME_LEN   1024
#define EVENT_SIZE      (sizeof(struct inotify_event))
#define BUF_LEN         (MAX_EVENTS * (EVENT_SIZE + FILE_NAME_LEN))


typedef map<int, string> WDS;
typedef mutex LOCK;
typedef lock_guard<mutex> LOCKGUARD;
typedef unique_lock<mutex> UNIQUEGUARD;


void exitHandler(int signal);
int processPdf(const std::string& dropDir, const std::string& convertDir,  const std::string& file);
int createPath(const std::string& rootPath, std::string& path, mode_t mode);
void handleEvents(int fd, WDS& wds, const string& rootDir, const string& dropDir, const string& convertDir);
int addWatch(int fd, const string& path, WDS& wds);
std::string fixPath(const std::string& dir);
int processExistingDirs(const string& rootdir);
int fswalkcb (const char * fileordir, const struct stat64 * fdstat, int, struct FTW*); // callback function used for directory
template <typename T> std::string xmlEscape(std::basic_string<T> input);
//void threadHandler();

string rootDir, dropDir, convertDir, ocrDir, storeDir ;
int fd = 0;
WDS wds;
LOCK mex;
atomic<bool> exitThreads;

#ifdef WITHTHREADPOOL
// Create pool with 3 threads
ThreadPool pool(5);
#endif

/*
 * A single or multithreaded (enable WITHTREADPOOL) file watcher + pdf to text converter (optionally uses OCR)
 */
int main(int argc, char** argv) 
{
    struct sigaction sigHandler;
    sigHandler.sa_handler = exitHandler;
    sigemptyset(&sigHandler.sa_mask);
    sigHandler.sa_flags = 0;
    sigaction(SIGINT, &sigHandler, NULL);
    
    int opt ;
    while ((opt = getopt(argc, argv, "r:d:c:o:s:")) != -1)
    {
        switch (opt)
        {
            case 'r':
                rootDir = optarg;
                rootDir = fixPath(rootDir);
                break;
            case 'd':
                dropDir = optarg;
                dropDir = fixPath(dropDir);
                break;
            case 'c':
                convertDir = optarg;
                convertDir = fixPath(convertDir);
                break;
            case 'o':
                ocrDir = optarg;
                ocrDir = fixPath(ocrDir);
                break;
            case 's':
                storeDir = optarg;
                storeDir = fixPath(storeDir);
                break;
            default:
                cerr << "USAGE: " << argv[0] << "-r rootdir -d dropdir -c convertdir -o ocrdir -s storedir \n";
                exit(EXIT_FAILURE);
        }
    }
    
    if (rootDir.empty() || storeDir.empty() || dropDir.empty() || convertDir.empty() || ocrDir.empty())
    {
        cerr << "USAGE: " << argv[0] << "-r rootdir -d dropdir -c convertdir -o ocrdir -s storedir \n";
        exit(EXIT_FAILURE);
    }        
    
    cout << "Beginning to monitor drop directory...." << endl;
    
    fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0)
    {
        cerr << "Failed to initialize inotify. Exiting program." << endl;
        exit(EXIT_FAILURE);
    }
    
    //thread thPdfProcessor(threadHandler);
    // Initialize pool
#ifdef WITHTHREADPOOL    
    pool.init();
#endif
    
    // mkdir for drop if not found and convertDir
    auto status = createPath(rootDir, dropDir, 0777);
    status = createPath(rootDir, convertDir, 0777);
    status = createPath(rootDir, ocrDir, 0777);
    status = createPath(rootDir, storeDir, 0777);
    string droppath = rootDir + "/" + dropDir;
    int wd = addWatch(fd, droppath, wds); // To watch directory creation inside drop directory.
    if (wd == -1)
    {
        cerr << "Failed to add watch with error " << strerror(errno) << ". Exiting program." << endl;
        goto CLEANUP;
    }
    
    processExistingDirs(rootDir + "/" + dropDir);
    
    struct pollfd fds[1]; // one for console input and other for inotify
    nfds_t nfds;
    char buf;
    int pollnums;
    
//    fds[0].fd = STDIN_FILENO;
//    fds[0].events = POLLIN;
    
    fds[0].fd = fd;
    fds[0].events = POLLIN;
    
    nfds = 1;
    
    while (true)
    {
        if (exitThreads)
            break;
        
        pollnums = poll(fds, nfds, -1);
        if (pollnums == -1)
        {
            if (errno = EINTR)
                continue;
            perror("Polling error.");
            exit(EXIT_FAILURE);
        }
        
        if (pollnums > 0)
        {
//            if (fds[0].revents & POLLIN)
//            {
//                while (read(STDIN_FILENO, &buf, 1) > 0 && 
//                        buf != 'q')
//                    continue;
//                exitThreads = true;
//            }
            if (fds[0].revents & POLLIN)
            {
                handleEvents(fd, wds, rootDir, dropDir, convertDir);
            }
        }
    }
    
    CLEANUP:
        for (auto wd : wds)
             inotify_rm_watch(fd, wd.first);
        close(fd);
        
        if (!exitThreads)
            exitThreads = true;
        //thPdfProcessor.join(); 
        
#ifdef WITHTHREADPOOL
        pool.shutdown();        
#endif
        
    return 0;
}

std::string fixPath(const std::string& dir)
{
    // remove / at the end if any
    if (dir.size() > 0)
    {
        auto ritr = dir.data()[dir.size()-1];
        if (ritr == '/')
            return dir.size() > 1 ? std::string(dir, 0, dir.size() - 1) : "";
    }
    return dir;
}

int addWatch(int fd, const string& path, WDS& wds)
{
    int wd = 0;
    bool hasIt = false;
    for (auto p : wds)
    {
        if (p.second == path)
        {
            hasIt = true;
            break;
        }
    }
    
    if (!hasIt)
    {
        wd = inotify_add_watch(fd, path.c_str(), IN_CREATE);
        if (wd == -1)
        {
            cerr << "Failed to add watch with error " << strerror(errno) << ". Exiting program." << endl;
        }
        else
        {
            wds.emplace(make_pair(wd, path));
        }
    }
    return wd;
}

int processExistingDirs(const string& rootdir)
{
    auto ret = nftw64(rootdir.c_str(), fswalkcb, MAX_DESCR, FTW_PHYS | FTW_MOUNT);
    if (ret < 0)
    {
        cout << "Failed to process files in sub directories under " << rootdir << endl;
        cout << strerror(errno) << endl;
    }
    return ret;
}

int fswalkcb(const char* fileordir, const struct stat64* fdstat, int ft, struct FTW*)
{
    auto fdir = (std::string)fileordir;
    cout << fdir << endl;
    switch (ft)
    {
        case FTW_D:
            // directory
            if (rootDir == (string)fileordir)
                return 0;
            addWatch(fd, fileordir, wds);
            break;
            
        case FTW_F:
            // file. Note that even system files such as sockets may also be reported.
            //docQueue.emplace(fileordir);
#ifdef WITHTHREADPOOL            
            pool.submit(processPdf, dropDir, convertDir, fdir);
#endif
            cout << "===========================================================" << endl;
            cout << "Preparing for processing " << fileordir << "." << endl;
            cout << "===========================================================" << endl;
#ifndef WITHTHREADPOOL            
            processPdf(dropDir, convertDir, fdir);
#endif           
            break;
    }
    return 0;
}

void handleEvents(int fd, WDS& wds, const string& rootDir, const string& dropDir, const string& convertDir)
{
    ssize_t len;
    int iidx;
    char buf[BUF_LEN];
    const struct inotify_event* event;
    char* ptr;
    // loop while events can be read from inotify fds
    for(;;)
    {
        len = read(fd, buf, BUF_LEN);
        if (len == -1 && errno != EAGAIN)
        {
            perror("Notify event: Read error");
            exit(EXIT_FAILURE);
        }
        if (len <= 0)
        {
            break;
        }
        
        for (ptr = buf; ptr < buf + len;
                ptr += sizeof(struct inotify_event) + event->len)
        {
            event = (const struct inotify_event*)ptr;
            if (event->mask & IN_CREATE)
            {
                if (event->mask & IN_ISDIR)
                {
                    // add this directory to watch list 
                    // if not already.
                    string newDir = rootDir + "/" + dropDir + "/" + event->name;
                    addWatch(fd, newDir, wds);
                    cout << "Created directory " << event->name;
                }
                else
                {
                    auto itrdir = wds.find(event->wd);
                    if (itrdir != wds.end())
                    {
                        cout << "File Name: " << itrdir->second + "/" + (string)event->name << endl;
                        // get directory
                        string filePath = itrdir->second + "/" + (string)event->name;
#ifdef WITHTHREADPOOL            
                        pool.submit(processPdf, dropDir, convertDir, filePath);
#endif
                        cout << "===========================================================" << endl;
                        cout << "Preparing for processing " << filePath << "." << endl;
                        cout << "===========================================================" << endl;
#ifndef WITHTHREADPOOL            
                        processPdf(dropDir, convertDir, filePath);
#endif
                    }
                }
            }
        }
    }
}

int processPdf(const std::string& dropDir, const std::string& convertDir, const std::string& file)
{
    
    bool outputBlocks = true;
    
    cout << "Thread Id: " << std::this_thread::get_id() << endl; 
    cout << "Starting the conversion of file " << file << "." << endl;
    
    // Convert PDF to image
    auto fpath = file;
    vector<string> splits;
    char* data = const_cast<char*>(fpath.data());
    auto tok = strtok(data, "/");
    while (tok)
    {
        splits.push_back((const char*)tok);
        tok = strtok(nullptr, "/");
    }
    
    auto supplId = splits[splits.size()-2];
    auto fileName = splits[splits.size()-1];
    
    auto ext = fileName.substr(fileName.rfind("."));
    
    if (ext != ".pdf")
    {
        return EXIT_FAILURE;
    }
    
    auto supplierDir = rootDir + "/" + convertDir + "/" + supplId;
    string fpathTxt = supplierDir + "/" + fileName;
    
    fpathTxt = fpathTxt.substr(0, fpathTxt.rfind(".")) + ".xml"; 
    
    createPath(rootDir + "/" + convertDir, supplId, 0777);
    createPath(rootDir + "/" + storeDir, supplId, 0777);
    
    ofstream ofs;
    ofs.open(fpathTxt, std::iostream::out | std::iostream::trunc);
    if (!ofs.is_open())
    {
        cout << "Error opening text file " << fpathTxt << endl;
        return 1;
    }
    
    document* pdf = document::load_from_file(file.c_str());
    cout << "Pdf has " << pdf->pages() << " pages." << endl;
    int pages = pdf->pages();
    std::vector<page*> vpages;
    ostringstream opdftxt;
    opdftxt << "<?xml version=\"1.0\" encoding=\"utf-8\"?>" << endl;
    opdftxt << "<conversioninfo>" << endl;
    opdftxt << "<fileinfo>" << endl;
    opdftxt << "<name>" << endl;
    opdftxt << fileName << endl;
    opdftxt << "</name>" << endl;
    opdftxt << "<supplierid>" << endl;
    opdftxt << supplId << endl;
    opdftxt << "</supplierid>" << endl;
    opdftxt << "</fileinfo>" << endl;
    for (int i=0; i < pages; i++)
    {
        auto pg = pdf->create_page(i);
        if (pg)
        {
            //auto img = new page_renderer()->render_page(pg);
            vpages.emplace_back(pg);
            
            if (!outputBlocks)
            {
                auto ustr = pg->text();
                cout << ustr.to_latin1() << endl;
                opdftxt << ustr.to_latin1() << endl;
            }
            else
            {
                TextBlockMap map;
                if (pg->textBlockMap(&map))
                {                
                    opdftxt << "<page num=\"" << i+1 << "\">" << endl;
                    for (auto pair : map)
                    {
                        opdftxt << "<block num=\"" << pair.first << "\">"  << endl;
                        for (auto p1 : pair.second)
                        {
                            opdftxt << "<line order=\"" << p1.first.POS << "\">" << endl;
                            opdftxt << "<pos>" << endl;
                            opdftxt << "<x>" << p1.first.X << "</x>" << endl;
                            opdftxt << "<y>" << p1.first.Y << "</y>" << endl;
                            opdftxt << "<w>" << p1.first.W << "</w>" << endl;
                            opdftxt << "<h>" << p1.first.H << "</h>" << endl;
                            opdftxt << "</pos>" << endl;
			    opdftxt << "<content>" << endl;
                            ustring ustr = ustring::from_latin1(p1.second.c_str());
                            //opdftxt << xmlEscape<char>(ustr.to_latin1());
                            opdftxt << ustr.to_latin1();
                            opdftxt << "</content>" << endl;
                            opdftxt << "</line>" << endl;
                        }
                        opdftxt << "</block>" << endl;
                    }
                }
            }
            opdftxt << "</page>" << endl;
        }
    }
    
    cout << opdftxt.str() << endl;
    
    std::vector<string> imgFiles;
    
    bool ocr = false;
    
    cout << "Size: " << opdftxt.str().size() << endl;
    if (opdftxt.str().size() < 200)
    {
        ocr = true;
        cout << "Text extract yielded only " << opdftxt.str().size() << " characters." << endl;
        cout << "Outputting OCR extraction \n" <<endl;
        for (int i=0; i < vpages.size(); i++)
        {
            auto pg = vpages.at(i);
            auto r = pg->page_rect();
            // convert to image.
            page_renderer* prender = new page_renderer();
            if (!prender->can_render())
            {
                cout << "Image render engine is not properly compiled." << endl;
                return 1;
            }
            //prender->set_paper_color(255);
            auto img = prender->render_page(pg, 300.0, 300.0);
            //auto supportedFormats = image::supported_image_formats();
            string dir = rootDir + "/" + ocrDir + "/" + supplId ;
            createPath(rootDir + "/" + ocrDir, supplId, 0777);
            ostringstream ostr;
            ostr << dir << "/" << fileName << "_" << i << ".pnm";
            auto result = img.save(ostr.str(), "pnm");
            cout << "Has saved ? " << result << endl;
            delete prender;
            delete pg;
            imgFiles.emplace_back(ostr.str());
        }
        cout << "OCR extraction completed." << endl;
    }
    else
    {
        opdftxt << "<convertedby>poppler</convertedby>" << endl;
        opdftxt << "</conversioninfo>" << endl;
        cout << "Text extraction yielded " << opdftxt.str().size() << " characters. OCR conversion not required." << endl;
        ofs << opdftxt.str();
    }
    
    vpages.clear();
    
    
    delete pdf;
    
    opdftxt.str("");
    
    TessBaseAPI* api = new TessBaseAPI();
    if (api->Init(NULL, NULL))
    {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }
    
    if (ocr)
    {
        opdftxt << "<?xml version=\"1.0\" encoding=\"utf-8\"?>" << endl;
        opdftxt << "<conversioninfo>" << endl;
        opdftxt << "<fileinfo>" << endl;
        opdftxt << "<name>" << endl;
        opdftxt << fileName << endl;
        opdftxt << "</name>" << endl;
        opdftxt << "<supplierid>" << endl;
        opdftxt << supplId << endl;
        opdftxt << "</supplierid>" << endl;
        opdftxt << "</fileinfo>" << endl;
    }
    
    int pagenum = 1;
    for (auto imgpath : imgFiles)
    {
        Pix* img = pixRead(imgpath.c_str());
        api->SetImage(img);
        api->SetSourceResolution(300);
        char* outText = api->GetUNLVText();
        printf("OCR output:\n%s", outText);
        opdftxt << "<page num=\"" << pagenum++ << "\">" << endl;
        opdftxt << xmlEscape<char>(outText) ;
        opdftxt << "</page>" << endl;
        delete [] outText;
        pixDestroy(&img);
    }
    
    if (ocr)
    {
        opdftxt << "<convertedby>ocr</convertedby>" << endl;
        opdftxt << "</conversioninfo>" << endl;
    }
    ofs << opdftxt.str();
    
    api->End();
    delete api;
    
    // move the pdf to store dir
    auto storeSupplDir = rootDir + "/" + storeDir + "/" + supplId + "/";
    storeSupplDir += file.substr(file.rfind("/") + 1);
    
    rename(file.c_str(), storeSupplDir.c_str());
    
    cout << "Completed conversion of file " << file << "." << endl;
    cout << "======================================================" << endl;
    return 0;
}

void exitHandler(int signal)
{
    exitThreads = true;
    return;
}

int createPath(const std::string& rootPath, std::string& path, mode_t mode )
{
    struct stat st;

    for( std::string::iterator iter = path.begin() ; iter != path.end(); )
    {
         std::string::iterator newIter = std::find( iter, path.end(), '/' );
         std::string newPath = rootPath + "/" + std::string( path.begin(), newIter);

         if( stat( newPath.c_str(), &st) != 0)
         {           
             if( mkdir( newPath.c_str(), mode) != 0 && errno != EEXIST )
             {
                std::cout << "cannot create folder [" << newPath << "] : " << strerror(errno) << std::endl;
                return -1;
             }
         }
         else
            if( !S_ISDIR(st.st_mode) )
             {
                 errno = ENOTDIR;
                 std:: cout << "path [" << newPath << "] not a dir " << std::endl;
                 return -1;
             }
             else
                 std::cout << "path [" << newPath << "] already exists " << std::endl;


         iter = newIter;
         if( newIter != path.end() )
             ++ iter;
    }
    return 0;
}

template <typename T> std::string xmlEscape(std::basic_string<T> input)
{
    std::ostringstream out;
    out.str("");
    for (auto it = input.begin(); it != input.end(); ++it)
    {
        auto c = *it;
        if (
                c == u'\x0' || 
                c == u'\xA' || 
                (c >= u'\x20' && c <= u'\xD7FF') ||
                (c >= u'\xE000' && c<= u'\xFFFD') 
                //||
                //(c >= u'\x10000' && c<= u'\x10FFFF')
            )
        {
            switch(c)
            {
                case '<':
                    out << "&lt;";
                    break;
                case '>':
                    out << "&gt;";
                    break;
                case '&':
                    out << "&amp;";
                    break;
                case '"':
                    out << "&quot;";
                    break;
                case '\'':
                    out << "&apos;";
                    break;
                default:
                    out << c ;
                    break;
            }
        }
        else
            out << ' ';
    }
    auto str = out.str();
    return str;
}

