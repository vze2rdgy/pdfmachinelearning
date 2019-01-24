import { AppState } from "@app/core";
import { createFeatureSelector, ActionReducerMap } from "@ngrx/store";
import { PaymentsHomeState } from "./payment.models";
import { paymentsReducer } from "./payment.reducers";

export const FEATURE_NAME = 'payments';
export const selectPayments = createFeatureSelector<State, PaymentsState>(
    FEATURE_NAME
);

export const reducers : ActionReducerMap<PaymentsState> ={
    home :paymentsReducer    
}

export interface PaymentsState{
    home: PaymentsHomeState,    
}

export interface State extends AppState{
    payments : PaymentsState
}