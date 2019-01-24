import { ConnectTemlatesState } from "./template.models";
import { ConnectActions, ConnectActionTypes } from "../connect.actions";


export const initialState: ConnectTemlatesState = {
    retrieveReqTimeStamp: null,
    templatesResponse: { templates: null, error: null }
}

export function templateReducer(
    state: ConnectTemlatesState = initialState,
    action: ConnectActions
): ConnectTemlatesState {
    switch (action.type) {
        case ConnectActionTypes.RETRIEVETEMPLS:
            return {
                ...state,
                retrieveReqTimeStamp: action.payload.timestamp,
                templatesResponse: { templates: null, error: null }
            }
        case ConnectActionTypes.RETRIEVETEMPLS_SUCCESS:
            return {
                ...state,
                templatesResponse: { templates: action.payload.templates, error: null }
            }
        case ConnectActionTypes.RETRIEVETEMPLS_ERROR:
            return {
                ...state,
                templatesResponse: { templates: null, error: action.payload.error }
            }
        default:
            return state;
    }
}