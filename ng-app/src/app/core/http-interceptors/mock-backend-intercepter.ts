import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HTTP_INTERCEPTORS } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { delay, mergeMap, materialize, dematerialize } from "rxjs/operators";
import { GetUserProfileJson } from "./mockJson/getuserprofile.mock.data";
import { fileUploadJson } from "./mockJson/fileUpload.mock.data";
import { GetStudentsJson } from "./mockJson/getStudents.mock.data";
import { GetPaymentCodeInfo } from "./mockJson/getpaymentcodeinfo.mock.data";
import { GenerateFamilyCodeJson } from "./mockJson/generatefamilycode.mock.data";
import { AddStudentJson } from "./mockJson/addStudent.mock.data";
import { StudentTuitionJson } from "./mockJson/tuitions.mock.data";
import { SettingJson } from "./mockJson/getSettings.mock.data";
import { BaseResponseJson } from "./mockJson/baseresponse.mock.data";
import { emailTemplates } from "./mockJson/getTemplates.mock.data";


export class MockBackendIntercepter implements HttpInterceptor {
    constructor() { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        console.log("Handled By Intercepter for URL " + request.url);

        return of(null).pipe(mergeMap(() => {
            console.log("Checking URL");

            if (request.url.endsWith("/api/getuserprofile") && request.method === "GET") {
                console.log("me here");
                return of(new HttpResponse(
                    {
                        status: 500,
                        body: GetUserProfileJson
                    }
                ));
            }

            if (request.url.includes("/upload") && request.method === "POST"){
                console.log("Mockup for upload");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: fileUploadJson
                    }
                ));
            } 

            
            if (request.url.includes("/students") && request.method === "GET"){
                console.log("Mockup for Students");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: GetStudentsJson
                    }
                ));
            } 

            if (request.url.includes("/paymentinfo") && request.method === "GET"){
                console.log("Mockup for /paymentinfo");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: GetPaymentCodeInfo
                    }
                ));
            } 


            if (request.url.includes("/gprn") && request.method === "POST"){
                console.log("Mockup for /gprn");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: GenerateFamilyCodeJson
                    }
                ));
            } 

            if (request.url.includes("/addStudent") && request.method === "POST"){
                console.log("Mockup for /addStudent");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: AddStudentJson
                    }
                ))
            }
            if (request.url.includes("/tuitions") && request.method === "GET"){
                console.log("Mockup for /tuitions");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: StudentTuitionJson
                    }
                ));
            } 
            if (request.url.includes("/tuitions") && request.method === "POST"){
                console.log("Mockup for /tuitions");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: BaseResponseJson
                    }
                ));
            }             
            if (request.url.includes("/settings") && request.method === "GET"){
                console.log("Mockup for /settings");
                return of(new HttpResponse(
                    {
                        status: 200,
                        body: SettingJson
                    }
                )); 
            } 

            if (request.url.includes("/settings") && request.method === "POST"){
                console.log("Mockup for /settings" );
                console.log("request + ->" + JSON.stringify(request.body ));

                return of(new HttpResponse(
                    {
                        status: 200,
                        body: BaseResponseJson
                    }
                )); 
            } 
            if (request.url.includes("/register") && request.method === "POST"){
                console.log("Mockup for /register" );
                console.log("request + ->" + JSON.stringify(request.body ));

                return of(new HttpResponse(
                    {
                        status: 200,
                        body: {status: false}
                    }
                )); 
            } 

            if (request.url.includes("/templates") && request.method === "GET"){
                console.log("Mockup for /templates" );
                //console.log("request + ->" + JSON.stringify(request.body ));

                return of(new HttpResponse(
                    {
                        status: 200,
                        body: emailTemplates
                    }
                )); 
            } 

            return next.handle(request);

        }))
            .pipe(materialize())
            .pipe(delay(1000))
            .pipe(dematerialize());
    }
}

