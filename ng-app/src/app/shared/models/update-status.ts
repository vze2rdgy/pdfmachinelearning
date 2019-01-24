import { BaseResponse } from "../base-response";
import { HttpErrorResponse } from "@angular/common/http";

export interface UpdateStatus{
    updatesucess?: BaseResponse;
    updateerror?: HttpErrorResponse; 
  }