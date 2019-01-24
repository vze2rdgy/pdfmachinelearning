import { StudentsHomeState } from "./home.model";
import { StudentsActions, StudentsActionTypes } from "./home.actions";

export const initialState: StudentsHomeState = {
    students: null,
    activeOnly: true,
    retrieveReqTimeStamp: null,
    error: null
}


export function studentsHomeReducer(
    state: StudentsHomeState = initialState,
    action: StudentsActions
): StudentsHomeState {

    switch (action.type) {
        case StudentsActionTypes.RETRIEVE:
            return {
                ...state,
                students: null,
                retrieveReqTimeStamp: action.payload.timestamp,
                error: null
            };

        case StudentsActionTypes.RETRIEVE_SUCCESS:
            return {
                ...state,
                students: action.payload.students,
                error: null,
            };

        case StudentsActionTypes.RETRIEVE_ERROR:
            return {
                ...state,
                students: null,
                retrieveReqTimeStamp: null,
                error: action.payload.error
            }
        case StudentsActionTypes.TOGGLEACTIVEONLY:
            return {
                ...state,
                activeOnly: action.payload.activeOnly
            }
        default:
            return state;
    }
}