import { Action } from "@ngrx/store";
import { UploadResponse } from "./upload-response";
import { HttpErrorResponse } from "@angular/common/http";

export enum UploadActionTypes {
    UPLOADSTUDENTS = '[Upload] Students',
    UPLOADSTUDENTS_SUCCESS = '[Upload] Students Success',
    UPLOADSTUDENTS_ERROR = '[Upload] Students Error',

    UPLOADTUITIONS = '[Upload] Tuitions',
    UPLOADTUITIONS_SUCCESS = '[Upload] Tuitions Success',
    UPLOADTUITIONS_ERROR = '[Upload] Tuitions Error',

    UPLOADCHECKTRN = '[Upload] Check tran',
    UPLOADCHECKTRN_SUCCESS = '[Upload] Check trn Success',
    UPLOADCHECKTRN_ERROR = '[Upload] Check trn Error',

    UPLOADCREDITTRN = '[Upload] Credit Trn',
    UPLOADCREDITTRN_SUCCESS = '[Upload] Credit TRN Success',
    UPLOADCREDITTRN_ERROR = '[Upload] CreditTrn Error',
}

export class ActionStudentUpload implements Action {
    readonly type = UploadActionTypes.UPLOADSTUDENTS;

    constructor(readonly payload: { file: File, mapping: string }) { }
}

export class ActionStudentsUploadSuccess implements Action {
    readonly type = UploadActionTypes.UPLOADSTUDENTS_SUCCESS;

    constructor(readonly payload: { uploadRes: UploadResponse}) { }
}

export class ActionStudentsUploadError implements Action {
    readonly type = UploadActionTypes.UPLOADSTUDENTS_ERROR;

    constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export type  UploadActions = 
ActionStudentUpload | ActionStudentsUploadSuccess | ActionStudentsUploadError;