import { AuthState, AuththorizationStatus } from './auth.models';
import { AuthActions, AuthActionTypes } from './auth.actions';

export const initialState: AuthState = {
  isAuthenticated: false,
  auththorizationStatus: AuththorizationStatus.PENDING,
  authProfile: null,
  selectedLocation: null
};

export function authReducer(
  state: AuthState = initialState,
  action: AuthActions
): AuthState {
  switch (action.type) {
    case AuthActionTypes.LOGIN:
      return { ...state, isAuthenticated: true };

    case AuthActionTypes.REQAUTHORIZATION:
      return { ...state, auththorizationStatus: AuththorizationStatus.PENDING, authProfile: null, selectedLocation: null };

    case AuthActionTypes.AUTHORIZE:
      return { ...state, auththorizationStatus: AuththorizationStatus.AUTHORIZED, authProfile: action.payload , selectedLocation: action.selectedLocation};

      case AuthActionTypes.CHANGELOCATION:
      return {...state, selectedLocation: action.payload }      

    case AuthActionTypes.UNAUTHORIZE:
      return { ...state, auththorizationStatus: AuththorizationStatus.UNAUTHORIZED, authProfile: action.payload, selectedLocation: null};

    case AuthActionTypes.LOGOUT:
      return { ...state, isAuthenticated: false, auththorizationStatus: AuththorizationStatus.UNAUTHORIZED, authProfile: null, selectedLocation: null };

      case AuthActionTypes.SESSIONENDED:
      return { ...state, isAuthenticated: false, auththorizationStatus: AuththorizationStatus.UNAUTHORIZED, authProfile: null, selectedLocation: null };

    default:
      return state;
  }
}
