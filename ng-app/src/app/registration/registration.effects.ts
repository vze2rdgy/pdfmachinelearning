import { Injectable } from "@angular/core";
import { Actions, Effect, ofType } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { RegisterService } from "./register.service";
import { ActionRegistrationRegister, RegistrationActionTypes, ActionRegistrationRegisterSucess, ActionRegistrationRegisterError } from "./registration.actions";
import { switchMap, map, catchError } from "rxjs/operators";
import { HttpErrorResponse } from "@angular/common/http";
import { of } from "rxjs";
import { ActionReqAuthorization } from "@app/core";

@Injectable()
export class RegistrationEffects {
    constructor(
        private actions$: Actions<Action>,
        private service: RegisterService
    ) { }

    @Effect()
    registerLocation = this.actions$.pipe(
        ofType<ActionRegistrationRegister>(RegistrationActionTypes.REGISTER),
        switchMap((action: ActionRegistrationRegister) =>
            this.service.registerLocation(action.payload.location).pipe(
                map(response => {
                    if (response.status === true) {
                        return new ActionReqAuthorization();
                    }
                    else {
                        return new ActionRegistrationRegisterError({ error: new HttpErrorResponse({ error: "Registration Failed" }) });
                    }
                }),
                catchError(error => {
                    return of(new ActionRegistrationRegisterError({ error: error }));
                })
            )
        )
    );

}