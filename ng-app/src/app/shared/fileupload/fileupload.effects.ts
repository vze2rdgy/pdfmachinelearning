import { Injectable } from "@angular/core";
import { Actions, Effect, ofType } from "@ngrx/effects";
import { Action } from "@ngrx/store";
import { FileuploadService } from "./fileupload.service";
import { ActionStudentUpload, UploadActionTypes, ActionStudentsUploadSuccess, ActionStudentsUploadError } from "./fileupload.actions";
import { switchMap, map, catchError } from "rxjs/operators";
import { of } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class UploadEffects {
    constructor(
        private actions$: Actions<Action>,
        public service: FileuploadService
    ) { }

    @Effect()
    uploadStudents = this.actions$.pipe(
        ofType<ActionStudentUpload>(UploadActionTypes.UPLOADSTUDENTS),
        switchMap((action: ActionStudentUpload) =>
            this.service.uploadFile(action.payload.file, action.payload.mapping, 1)
                .pipe(
                    map(response => {
                        console.log("bs");
                        return new ActionStudentsUploadSuccess({ uploadRes: response });
                    }),
                    catchError(error => {
                        return of(new ActionStudentsUploadError({ error: error }));
                    })
                )
        )
    );
    @Effect()
    uploadTiotions = this.actions$.pipe(
        ofType<ActionStudentUpload>(UploadActionTypes.UPLOADTUITIONS),
        switchMap((action: ActionStudentUpload) =>
            this.service.uploadFile(action.payload.file, action.payload.mapping, 1)
                .pipe(
                    map(response => {
                        return new ActionStudentsUploadSuccess({ uploadRes: response });
                    }),
                    catchError(error => {
                        return of(new ActionStudentsUploadError({ error: error }));
                    })
                )
        )
    );
}