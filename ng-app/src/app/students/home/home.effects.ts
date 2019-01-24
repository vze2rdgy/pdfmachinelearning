import { Injectable } from "@angular/core";
import { Actions, Effect, ofType } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { StudentsService } from "../students.service";
import { ActionStudentsRetrieve, StudentsActionTypes, ActionStudentsRetrieveSuccess, ActionStudentsRetrieveError } from "./home.actions";
import { tap, switchMap, map, catchError } from "rxjs/operators";
import { of } from "rxjs";


@Injectable()
export class StudentsHomeEffects {
    constructor(
        private actions$: Actions<Action>,
        private service: StudentsService
    ) { }

    @Effect()
    retrieveStudentsHome = this.actions$.pipe(
        ofType<ActionStudentsRetrieve>(StudentsActionTypes.RETRIEVE),
        switchMap((action: ActionStudentsRetrieve) =>
            this.service.getStudentBasicInfo().pipe(
               map(studentBasicInfos =>{
                    return new ActionStudentsRetrieveSuccess({students: studentBasicInfos});
               }),
               catchError( error => {
                   return of(new ActionStudentsRetrieveError({error: error}));
               })
            )
        )
    );
}