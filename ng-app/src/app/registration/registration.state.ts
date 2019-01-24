import { AppState } from "@app/core";
import { HttpErrorResponse } from "@angular/common/http";
import { createFeatureSelector, ActionReducerMap } from "@ngrx/store";

export const FEATURE_NAME = 'registration';

export const selectRegistration = createFeatureSelector<State, RegistrationState>(
    FEATURE_NAME
);

export interface RegistrationState {
    status: Boolean,
    error?: HttpErrorResponse
}

export interface State extends AppState {
    registration: RegistrationState
}