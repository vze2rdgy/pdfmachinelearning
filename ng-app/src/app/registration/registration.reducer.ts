import { RegistrationState } from "./registration.state";
import { RegistrationActions, RegistrationActionTypes } from "./registration.actions";

export const initialState: RegistrationState = {
    status: false,
    error: null
}

export function registrationReducer(
    state: RegistrationState = null,
    action: RegistrationActions
): RegistrationState {

    switch (action.type) {
        case RegistrationActionTypes.REGISTER:
            return {
                ...state,
                status: false,
                error: null
            }
        case RegistrationActionTypes.REGISTER_SUCCESS:
            return {
                ...state,
                status: true,
                error: null
            }
        case RegistrationActionTypes.REGISTER_ERROR:
            return {
                ...state,
                status: false,
                error: action.payload.error
            }
        default:
            return state;
    }
}