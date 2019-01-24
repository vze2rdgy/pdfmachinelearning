import { SettingsState, NIGHT_MODE_THEME } from './settings.model';
import { SettingsActions, SettingsActionTypes } from './settings.actions';

export const initialState: SettingsState = {
  language: 'en',
  theme: 'DEFAULT-THEME',
  autoNightMode: false,
  nightTheme: NIGHT_MODE_THEME,
  stickyHeader: true,
  pageAnimations: true,
  pageAnimationsDisabled: false,
  elementsAnimations: true,
  hour: 0,
  locationdetails: [],
  lcoationretrieveerror: null,
  updateStatus: null
};

export function settingsReducer(
  state: SettingsState = initialState,
  action: SettingsActions
): SettingsState {
  switch (action.type) {
    case SettingsActionTypes.CHANGE_LANGUAGE:
    case SettingsActionTypes.CHANGE_THEME:
    case SettingsActionTypes.CHANGE_AUTO_NIGHT_AUTO_MODE:
    case SettingsActionTypes.CHANGE_STICKY_HEADER:
    case SettingsActionTypes.CHANGE_ANIMATIONS_PAGE:
    case SettingsActionTypes.CHANGE_ANIMATIONS_ELEMENTS:
    case SettingsActionTypes.CHANGE_HOUR:
      return { ...state, ...action.payload };

    case SettingsActionTypes.CHANGE_ANIMATIONS_PAGE_DISABLED:
      return {
        ...state,
        pageAnimations: false,
        pageAnimationsDisabled: action.payload.pageAnimationsDisabled
      };

    case SettingsActionTypes.RETRIEVE:
      return {
        ...state,
        locationdetails: []
      }
    case SettingsActionTypes.RETRIEVE_SUCCESS:
      return {
        ...state,
        locationdetails: action.payload.settings,
        lcoationretrieveerror: null
      }
    case SettingsActionTypes.RETRIEVE_ERROR:
      return {
        ...state,
        locationdetails: null,
        lcoationretrieveerror: action.payload.error
      }
    case SettingsActionTypes.UPDATE:
      return {
        ...state,
        updateStatus: { updatesucess: null, updateerror: null }
      }
    case SettingsActionTypes.UPDATE_SUCCESS:
      return {
        ...state,
        updateStatus: { updatesucess: action.payload.data, updateerror: null }
      }
    case SettingsActionTypes.UPDATE_ERROR:
      return {
        ...state,
        updateStatus: { updatesucess: null, updateerror: action.payload.error }
      }
    default:
      return state;
  }
}
