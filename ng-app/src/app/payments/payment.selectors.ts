import { createSelector } from "@ngrx/store";
import { selectPayments, PaymentsState } from "./payments.state";
import { PaymentsHomeState } from "./payment.models";

export const selectPaymentsState = createSelector(
    selectPayments,
    (state: PaymentsState) => state.home
);

export const selectPaymentsHomeRes = createSelector(
    selectPaymentsState,
    (state: PaymentsHomeState) => state.paymentInfoResponse
);
