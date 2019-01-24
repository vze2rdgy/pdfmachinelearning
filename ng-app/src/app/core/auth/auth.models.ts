import { AuthProfile, Loc } from "./auth-profile";

export enum AuththorizationStatus{
  PENDING = 0,
  UNAUTHORIZED = 1,
  AUTHORIZED = 2
}

export interface AuthState {
  isAuthenticated: boolean;
  auththorizationStatus: AuththorizationStatus;
  authProfile: AuthProfile;
  selectedLocation?: Loc;
}
