import { HttpErrorResponse } from "@angular/common/http";

//requiredCols & colsRecieved will be "," saperated string
export interface UploadResponse {
    status: string;
    requiredCols: string;
    colsRecieved: string;
    message: string;
}

export interface FileUploadState {
    studentsUpldRes?: UploadResponse;
    tuitionsUpldRes?: UploadResponse;
    checkTranUpldRes?: UploadResponse;
    creditTranUpldRes?: UploadResponse;

    studentUpldError?: HttpErrorResponse;
    tuitionsUpldError?: HttpErrorResponse;
    checkTrnUpldError?: HttpErrorResponse;
    creditTrnUpldError?: HttpErrorResponse;

}