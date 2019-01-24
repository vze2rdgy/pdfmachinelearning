import { HttpErrorResponse } from "@angular/common/http";
import { BaseResponse } from "@app/shared";
import { UpdateStatus } from "@app/shared/models/update-status";

export interface Tuition {
    fname?: string;
    lname?: string;
    studentid?: string;
    math?: number;
    reading?: number;
    locationid?: number;
  }

  export interface TuitionsState{
      tuitions?: Tuition[]
      retrieveReqTimeStamp?: string;
      error?: HttpErrorResponse;  

      update?: any;
      updateStatus?: UpdateStatus;

  }
