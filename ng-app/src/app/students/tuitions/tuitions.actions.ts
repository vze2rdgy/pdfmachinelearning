import { Tuition } from "./tuitions.model";
import { Action } from "@ngrx/store";
import { HttpErrorResponse } from "@angular/common/http";
import { BaseResponse } from "@app/shared";

export enum TuitionsActionTypes {
  RETRIEVE = '[Tuitions] Retrieve',
  RETRIEVE_SUCCESS = '[Tuitions] Retrieve Success',
  RETRIEVE_ERROR = '[Tuitions] Retrieve Error',

  UPDATE = '[Tuitions] Update',
  UPDATE_SUCCESS = '[Tuitions] Update Success',
  UPDATE_ERROR = '[Tuitions] Update Error',

}

export class ActionTuitionsRetrieve implements Action {
  readonly type = TuitionsActionTypes.RETRIEVE;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { timestamp: string }) { }
}

export class ActionTuitionsRetrieveSuccess implements Action {
  readonly type = TuitionsActionTypes.RETRIEVE_SUCCESS;

  constructor(readonly payload: { tuitions: Tuition[] }) { }
}

export class ActionTuitionsRetrieveError implements Action {
  readonly type = TuitionsActionTypes.RETRIEVE_ERROR;

  constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export class ActionTuitionsUpdate implements Action {
  readonly type = TuitionsActionTypes.UPDATE;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { data: any }) { }
}
export class ActionTuitionsUpdateSuccess implements Action {
  readonly type = TuitionsActionTypes.UPDATE_SUCCESS;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { data: BaseResponse }) { }
}

export class ActionTuitionsUpdateError implements Action {
  readonly type = TuitionsActionTypes.UPDATE_ERROR;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export type TuitionsActions =
  | ActionTuitionsRetrieve
  | ActionTuitionsRetrieveSuccess
  | ActionTuitionsRetrieveError

  | ActionTuitionsUpdate
  | ActionTuitionsUpdateSuccess
  | ActionTuitionsUpdateError;


