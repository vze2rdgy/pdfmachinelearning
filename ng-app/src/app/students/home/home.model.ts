import { HttpErrorResponse } from "@angular/common/http";

export interface StudentBasicInfo {
    dob?: string;
    email?: string;
    gradelevel?: string;
    locationid?: number;
    name?: string;
    paymentcode?: string;
    paymentcodedue?: number;
    paymentrecieved?: number;
    studentid?: string;
    subjects?: string;
    totalfee?: number;    
}

export interface StudentsHomeState{
    students? : StudentBasicInfo[];
    activeOnly: Boolean;
    retrieveReqTimeStamp?: string;
    error?: HttpErrorResponse;
}