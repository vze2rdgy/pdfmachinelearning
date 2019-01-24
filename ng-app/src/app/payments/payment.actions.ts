import { Action } from "@ngrx/store";
import { HttpErrorResponse } from "@angular/common/http";
import { PaymentcodeInfo } from "./payment.models";

export enum PaymentsActionTypes{
    RETRIEVE = '[Payments] Retrieve',
    RETRIEVE_SUCCESS = '[Payments] Retrieve Success',
    RETRIEVE_ERROR = '[Payments] Retrieve Error'
}

export class ActionPaymentsRetrieve implements Action {
    readonly type = PaymentsActionTypes.RETRIEVE;
  
    //TODO: timestamp should be a date time. 
    constructor(readonly payload: { timestamp: string }) {}
  }
  
  export class ActionPaymentsRetrieveSuccess implements Action {
    readonly type = PaymentsActionTypes.RETRIEVE_SUCCESS;
  
    constructor(readonly payload: { payments: PaymentcodeInfo[] }) {}
  }
  
  export class ActionPaymentsRetrieveError implements Action {
    readonly type = PaymentsActionTypes.RETRIEVE_ERROR;
  
    constructor(readonly payload: { error?: HttpErrorResponse }) {}
  }


  export type PaymentsActions =
    | ActionPaymentsRetrieve
    | ActionPaymentsRetrieveSuccess
    | ActionPaymentsRetrieveError;  