import { createFeatureSelector, ActionReducerMap } from "@ngrx/store";

import { AppState } from "@app/core";
import { fileUploadReducer } from "./fileupload/fileupload.reducers";
import { FileUploadState } from "./fileupload/upload-response";

export const FEATURE_NAME = 'shared';

export const selectFileUpload = createFeatureSelector<State, SharedState>(
    FEATURE_NAME
);

export const reducers : ActionReducerMap<SharedState> ={
    upload: fileUploadReducer
}

export interface SharedState{
    upload: FileUploadState,    
}
export interface State extends AppState{
    shared : SharedState
}
