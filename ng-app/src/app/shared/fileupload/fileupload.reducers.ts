import { FileUploadState } from "./upload-response";
import { UploadActions, UploadActionTypes } from "./fileupload.actions";

export const initialState: FileUploadState = {
    studentsUpldRes: null,
    studentUpldError: null,

    tuitionsUpldRes: null,
    tuitionsUpldError: null,

    checkTranUpldRes: null,
    checkTrnUpldError: null,

    creditTranUpldRes: null,
    creditTrnUpldError: null
}


export function fileUploadReducer(
    state: FileUploadState = initialState,
    action: UploadActions
): FileUploadState {
    switch (action.type) {
        case UploadActionTypes.UPLOADSTUDENTS:
        console.log("as");
            return {
                ...state,
                studentsUpldRes: null,
                studentUpldError: null
            };

        case UploadActionTypes.UPLOADSTUDENTS_SUCCESS:
            return {
                ...state,
                studentsUpldRes: action.payload.uploadRes,
                studentUpldError: null,
            };

        case UploadActionTypes.UPLOADSTUDENTS_ERROR:
            return {
                ...state,
                studentsUpldRes: null,
                studentUpldError: action.payload.error
            }
        default:
            return state;
    }
}