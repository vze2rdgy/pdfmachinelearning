import { selectStudents, StudentsState } from "../student.state";
import { createSelector } from "@ngrx/store";
import { StudentBasicInfo, StudentsHomeState } from "./home.model";

export const selectStudentsHomeState = createSelector(
    selectStudents,
    (state: StudentsState) => state.home
);

export const selectStudentsHomeItems = createSelector(
    selectStudentsHomeState,
    (state: StudentsHomeState) => state.students
);


export const selectStudentsHomeActiveOnly = createSelector(
    selectStudentsHomeState,
    state => state.activeOnly
);

export const selectStudentsHomeStudentFiltered = createSelector(
    selectStudentsHomeItems,    
    selectStudentsHomeActiveOnly,
    (students, activeOnly) => {        
        if (students != null && activeOnly) {
            var filteredStudents: StudentBasicInfo[] = students.filter(s => (s.subjects != null && s.subjects.length > 0));
            return filteredStudents;
        } else {
            return students;
        }
    }
);
