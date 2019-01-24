import { Injectable } from "@angular/core";
import { Actions, ofType, Effect } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { ConnectService } from "../connect.service";
import { ConnectActionTypes, ActionConnectTemplRetrieve, ActionConnectTemplRetrieveSuccess, ActionConnectTemplRetrieveError } from "../connect.actions";
import { switchMap, catchError, map } from "rxjs/operators";
import { Template } from "@angular/compiler/src/render3/r3_ast";
import { of } from "rxjs";

@Injectable()
export class TemplateEffects {
    constructor(
        private actions$: Actions<Action>,
        private service: ConnectService
    ) { }
    @Effect()
    retrieveTemplates = this.actions$.pipe(
        ofType<ActionConnectTemplRetrieve>(ConnectActionTypes.RETRIEVETEMPLS),
        switchMap((action: ActionConnectTemplRetrieve) =>
            this.service.getTemplates().pipe(
                map(templates => {
                    return new ActionConnectTemplRetrieveSuccess({ templates: templates });
                }),
                catchError(error => {
                    return of(new ActionConnectTemplRetrieveError({ error: error }));
                })
            )
        )
    );
}