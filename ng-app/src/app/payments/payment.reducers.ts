import { PaymentsHomeState } from "./payment.models";
import { PaymentsActions, PaymentsActionTypes } from "./payment.actions";

export const initialState: PaymentsHomeState = {
    paymentInfoResponse :{paymentcodeInfos: null, error: null},
    retrieveReqTimeStamp: null
}


export function paymentsReducer(
    state: PaymentsHomeState = initialState,
    action: PaymentsActions
): PaymentsHomeState {

    switch (action.type) {
        case PaymentsActionTypes.RETRIEVE:
            return {
                ...state,
                paymentInfoResponse :{paymentcodeInfos: null, error: null},
                retrieveReqTimeStamp: action.payload.timestamp,
            };

        case PaymentsActionTypes.RETRIEVE_SUCCESS:
            return {
                ...state,
                paymentInfoResponse :{paymentcodeInfos: action.payload.payments, error: null},
            };

        case PaymentsActionTypes.RETRIEVE_ERROR:
            return {
                ...state,
                paymentInfoResponse :{paymentcodeInfos: null, error: action.payload.error},
                retrieveReqTimeStamp: null,
            }
        default:
            return state;
    }
}