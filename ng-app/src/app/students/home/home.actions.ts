import { StudentBasicInfo } from "./home.model";
import { Action } from "@ngrx/store";
import { HttpErrorResponse } from "@angular/common/http";

export enum StudentsActionTypes{
    RETRIEVE = '[Students] Retrieve',
    RETRIEVE_SUCCESS = '[Students] Retrieve Success',
    RETRIEVE_ERROR = '[Students] Retrieve Error',
    TOGGLEACTIVEONLY = '[Students] Toggle ActiveOnly'
}

export class ActionStudentsRetrieve implements Action {
    readonly type = StudentsActionTypes.RETRIEVE;
  
    //TODO: timestamp should be a date time. 
    constructor(readonly payload: { timestamp: string }) {}
  }
  
  export class ActionStudentsRetrieveSuccess implements Action {
    readonly type = StudentsActionTypes.RETRIEVE_SUCCESS;
  
    constructor(readonly payload: { students: StudentBasicInfo[] }) {}
  }
  
  export class ActionStudentsRetrieveError implements Action {
    readonly type = StudentsActionTypes.RETRIEVE_ERROR;
  
    constructor(readonly payload: { error?: HttpErrorResponse }) {}
  }

  export class ActionStudentsToggleActiveOnly implements Action {
    readonly type = StudentsActionTypes.TOGGLEACTIVEONLY;
    constructor(readonly payload: { activeOnly: Boolean }) {}
  }

  export type StudentsActions =
    | ActionStudentsRetrieve
    | ActionStudentsRetrieveSuccess
    | ActionStudentsRetrieveError
    | ActionStudentsToggleActiveOnly;
  