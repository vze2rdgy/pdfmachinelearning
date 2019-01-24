import { Injectable } from "@angular/core";
import { Actions, Effect, ofType } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { StudentsService } from "../students.service";
import { TuitionsActionTypes, ActionTuitionsRetrieve, ActionTuitionsRetrieveSuccess, ActionTuitionsRetrieveError, ActionTuitionsUpdate, ActionTuitionsUpdateSuccess, ActionTuitionsUpdateError } from "./tuitions.actions";
import { switchMap, catchError, map } from "rxjs/operators";
import { of } from "rxjs";

@Injectable()
export class TuitionsEffects {
    constructor(
        private actions$: Actions<Action>,
        private service: StudentsService
    ) { }

    @Effect()
    retrieveTuitions = this.actions$.pipe(
        ofType<ActionTuitionsRetrieve>(TuitionsActionTypes.RETRIEVE),
        switchMap((action: ActionTuitionsRetrieve) =>
            this.service.getTuitions().pipe(
                map(tuitions => {
                    return new ActionTuitionsRetrieveSuccess({ tuitions: tuitions });
                }),
                catchError(error => {
                    return of(new ActionTuitionsRetrieveError({ error: error }));
                })
            )
        )
    );


    @Effect()
    updateTuitions = this.actions$.pipe(
        ofType<ActionTuitionsUpdate>(TuitionsActionTypes.UPDATE),
        switchMap((action: ActionTuitionsUpdate) =>
            this.service.UpdateTuitions(action.payload.data).pipe(
                map(response => {
                    return new ActionTuitionsUpdateSuccess({ data: response });
                },
                    catchError(error => {
                        return of(new ActionTuitionsUpdateError({ error: error }));
                    })
                )
            )
        )
    );

}