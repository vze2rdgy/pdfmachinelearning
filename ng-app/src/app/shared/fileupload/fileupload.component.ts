import { Component, OnInit, Input, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { FileuploadService } from './fileupload.service';

import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { UploadResponse } from './upload-response';
import { NotificationService, AppState, selectIsAuthenticated, ActionAuthLogin, ActionAuthLogout } from '@app/core';
import { take } from 'rxjs/operators';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { State } from '../shared.state';
import { ActionStudentUpload, ActionStudentsUploadSuccess } from './fileupload.actions';

@Component({
  selector: 'app-fileupload',
  templateUrl: './fileupload.component.html',
  styleUrls: ['./fileupload.component.scss'],
})
export class FileuploadComponent implements OnInit {

  @Input('filetype') fileType: number;
  @Input('title') title: string;
  @Input('subtitle') subtitle: string;
  @Input('reqcols') requiredCols: string[];
  colsInExcel: string[];
  mappedCols: string[] = [];


  mapping: string;
  message: string;

  fileToUpload: File = null;
  fileUploadInProgress = false;
  mappingrequired: boolean = false;


  constructor(
    private service: FileuploadService,
    private readonly notificationService: NotificationService,
    private store: Store<State>,
    private cdf: ChangeDetectorRef
  ) {
  }

  ngOnInit() {
    console.log("filetype = " + this.fileType);
    console.log("title = " + this.title);
    console.log("requiredCols = " + this.requiredCols);

    switch (this.fileType) {
      case 1:


      default:



    }
  }
  // drop(event: CdkDragDrop<string[]>) {
  //   moveItemInArray(this.requiredCols, event.previousIndex, event.currentIndex);
  // }
  drop(event: CdkDragDrop<string[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex);
    }
  }

  handleFileInput(files) {

    this.fileToUpload = files.item(0);
    console.log(files.item(0).name);
  }

  UploadFile() {
    console.log("Upload filetype = " + this.fileType);
    if (this.fileType != 0) {
      console.log("Uploading file ..." + this.fileToUpload.name);
      this.fileUploadInProgress = true;

      if (this.mappingrequired && this.mappedCols.length == this.requiredCols.length) {
        this.mapping = "{ "
        this.requiredCols.map((rcol, index) => {
          this.mapping += "\"" + rcol.trim() + "\" : \"" + this.mappedCols[index].trim() + "\"";
          if (index < this.mappedCols.length - 1) {
            this.mapping += ", ";
          }
        });
        this.mapping += "}"
      }

      console.log(this.mapping);

      this.service.uploadFile(this.fileToUpload, this.mapping, this.fileType)
        .pipe(take(1))
        .subscribe((response: UploadResponse) => {

          console.log("Upload File" + response);

          this.colsInExcel = response.colsRecieved.split(",");
          this.requiredCols = response.requiredCols.split(",");
          this.message = response.message;

          this.fileUploadInProgress = false;

          console.log("I am done with ->" + this.fileUploadInProgress + " ]");


          //review the status code
          if (response.status == "MISSINGREQIFIELDS") {
          } else if (response.status == "MISSINGMAPPING") {
            this.mappingrequired = true;
          } else {
            //success
            this.fileToUpload = null;
          }
          this.cdf.detectChanges();
          this.notificationService.info(response.message);

        });
    }
  }
}
