import { HttpErrorResponse } from "@angular/common/http";

export class Transaction {
    locationid: number;
    tranid: string;
    date: string;
    amount: number;
    payee: string;
    status: string;
    authno: string;
    paymentcode: string;
    paymenttype: string;
}

export class PaymentcodeInfo {
    paymentcode: string;
    locationid: number;
    paymentrecieved: number;
    paymentcodedue: number;
    // students: StudentBasicInfo[];
    trans: Transaction[];
    flagged: string;
}

export interface PaymentsHomeState{
    retrieveReqTimeStamp?: string;
    paymentInfoResponse? : PaymentInfoResponse;
}
    
export interface PaymentInfoResponse{
    paymentcodeInfos? : PaymentcodeInfo[];    
    error?: HttpErrorResponse;
}