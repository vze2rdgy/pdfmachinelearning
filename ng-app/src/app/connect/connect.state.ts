import { AppState } from "@app/core";
import { createFeatureSelector, ActionReducerMap } from "@ngrx/store";
import { ConnectTemlatesState } from "./templates/template.models";
import { templateReducer } from "./templates/template.reducers";

export const FEATURE_NAME = 'connect';
export const selectConnect = createFeatureSelector<State, ConnectState>(
    FEATURE_NAME
);

export const reducers : ActionReducerMap<ConnectState> = {
    templateState: templateReducer    
}

export interface ConnectState {
    templateState: ConnectTemlatesState
}

export interface State extends AppState {
    connect: ConnectState
}