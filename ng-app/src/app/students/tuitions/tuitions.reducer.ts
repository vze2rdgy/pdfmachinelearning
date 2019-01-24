import { TuitionsState } from "./tuitions.model";
import { TuitionsActions, TuitionsActionTypes } from "./tuitions.actions";

export const initialState: TuitionsState = {
    tuitions: null,
    retrieveReqTimeStamp: null,
    error: null,
    update: null,
    updateStatus: null
}

export function tuitionsReducer(
    state: TuitionsState = initialState,
    action: TuitionsActions
): TuitionsState {
    switch (action.type) {
        case TuitionsActionTypes.RETRIEVE:
            return {
                ...state,
                tuitions: null,
                retrieveReqTimeStamp: action.payload.timestamp,
                error: null
            }
        case TuitionsActionTypes.RETRIEVE_SUCCESS:
            return {
                ...state,
                tuitions: action.payload.tuitions,
                error: null
            }
        case TuitionsActionTypes.RETRIEVE_ERROR:
            return {
                ...state,
                tuitions: null,
                retrieveReqTimeStamp: null,
                error: action.payload.error
            }

        case TuitionsActionTypes.UPDATE:
            return {
                ...state,
                update: action.payload.data,
                updateStatus: null
            }
        case TuitionsActionTypes.UPDATE_SUCCESS:
            return {
                ...state,
                updateStatus : {updateerror: null, updatesucess: action.payload.data}
            }
        case TuitionsActionTypes.UPDATE_ERROR:
            return {
                ...state,
                updateStatus : {updateerror: action.payload.error, updatesucess: null}
            }
        default:
            return state;
    }
}