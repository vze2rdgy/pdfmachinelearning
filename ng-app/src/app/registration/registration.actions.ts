import { Action } from "@ngrx/store";
import { CenterLocation } from "./center-location";
import { HttpErrorResponse } from "@angular/common/http";

export enum RegistrationActionTypes {
    REGISTER = '[Registration] Register',
    REGISTER_SUCCESS = '[Registration] Sucess',
    REGISTER_ERROR = '[Registration] Error'
}

export class ActionRegistrationRegister implements Action {
    readonly type = RegistrationActionTypes.REGISTER;
    constructor(readonly payload: { location: CenterLocation }) { }
}

export class ActionRegistrationRegisterSucess implements Action {
    readonly type = RegistrationActionTypes.REGISTER_SUCCESS;
}

export class ActionRegistrationRegisterError implements Action {
    readonly type = RegistrationActionTypes.REGISTER_ERROR;
    constructor(readonly payload: { error?: HttpErrorResponse }) { }
}


export type RegistrationActions =
    ActionRegistrationRegister | ActionRegistrationRegisterSucess | ActionRegistrationRegisterError;