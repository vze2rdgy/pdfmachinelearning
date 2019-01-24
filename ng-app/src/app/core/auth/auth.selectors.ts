import { createSelector } from '@ngrx/store';

import { AuthState } from './auth.models';
import { selectAuthState } from '../core.state';

export const selectAuth = createSelector(
  selectAuthState,
  (state: AuthState) => state
);

export const selectIsAuthenticated = createSelector(
  selectAuthState,
  (state: AuthState) => state.isAuthenticated
);

export const selectAuthorization = createSelector(
  selectAuthState,
  (state: AuthState) => state.auththorizationStatus
);

export const selectAuthProfile = createSelector(
  selectAuthState,
  (state: AuthState) => state.authProfile
);

export const selectAuthLocationIds = createSelector(
  selectAuthState,
  (state: AuthState) => state.authProfile.locids
);

export const selectCurrentLocation = createSelector(
  selectAuthState,
  (state: AuthState) => state.selectedLocation
);

export const selectAuthUserEmail = createSelector(
  selectAuthState,
  (state: AuthState) => state.authProfile.userinfo.email
);

export const selectAuthUserName = createSelector(
  selectAuthState,
  (state: AuthState) => state.authProfile.userinfo.given_name
);