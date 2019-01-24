import { createFeatureSelector, ActionReducerMap } from "@ngrx/store";
import { AppState } from "@app/core";
import { StudentsHomeState } from "./home/home.model";
import {studentsHomeReducer} from './home/home.reducer';
import { tuitionsReducer } from "./tuitions/tuitions.reducer";
import { TuitionsState } from "./tuitions/tuitions.model";

export const FEATURE_NAME = 'students';
export const selectStudents = createFeatureSelector<State, StudentsState>(
    FEATURE_NAME
);

export const reducers : ActionReducerMap<StudentsState> ={
    home :studentsHomeReducer,
    tuitions: tuitionsReducer
}

export interface StudentsState{
    home: StudentsHomeState,
    tuitions : TuitionsState 
}

export interface State extends AppState{
    students : StudentsState
}
