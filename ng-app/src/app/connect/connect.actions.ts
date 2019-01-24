import { Action } from "@ngrx/store";
import { HttpErrorResponse } from "@angular/common/http";
import { Template } from "./templates/template.models";

export enum ConnectActionTypes {
    RETRIEVETEMPLS = '[Connect] Templates Retrieve',
    RETRIEVETEMPLS_SUCCESS = '[Connect] Templates Retrieve Success',
    RETRIEVETEMPLS_ERROR = '[Connect] Templates Retrieve Error'
}

export class ActionConnectTemplRetrieve implements Action {
    readonly type = ConnectActionTypes.RETRIEVETEMPLS;
    constructor(readonly payload: { timestamp: string }) { }
}
export class ActionConnectTemplRetrieveSuccess implements Action {
    readonly type = ConnectActionTypes.RETRIEVETEMPLS_SUCCESS;
    constructor(readonly payload: { templates: Template[] }) { }
}
export class ActionConnectTemplRetrieveError implements Action {
    readonly type = ConnectActionTypes.RETRIEVETEMPLS_ERROR;
    constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export type ConnectActions =
    | ActionConnectTemplRetrieve
    | ActionConnectTemplRetrieveSuccess
    | ActionConnectTemplRetrieveError;
