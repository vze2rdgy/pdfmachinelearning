import { selectStudents, StudentsState } from "../student.state";
import { createSelector } from "@ngrx/store";
import {TuitionsState} from './tuitions.model'

export const selectTuitionsState = createSelector(
    selectStudents,
    (state: StudentsState) => state.tuitions
);

export const selectTuitions = createSelector(
    selectTuitionsState,
    (state: TuitionsState) => state.tuitions
);

export const selectUpdateRes = createSelector(
    selectTuitionsState,
    (state: TuitionsState) => state.updateStatus
);