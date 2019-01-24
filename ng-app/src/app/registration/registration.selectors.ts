import { createSelector } from "@ngrx/store";
import { selectRegistration, RegistrationState } from "./registration.state";

export const selectRegistrationsState = createSelector(
    selectRegistration,
    (state: RegistrationState) => state
);

