import { Action } from '@ngrx/store';

import { Language } from './settings.model';
import { Setting } from '@app/shared/models/setting';
import { HttpErrorResponse } from '@angular/common/http';
import { BaseResponse } from '@app/shared';

export enum SettingsActionTypes {
  RETRIEVE = '[Settings] Retrieve',
  RETRIEVE_SUCCESS = '[Settings] Retrieve Success',
  RETRIEVE_ERROR = '[Settings] Retrieve Error',
  CHANGE_LANGUAGE = '[Settings] Change Language',
  CHANGE_THEME = '[Settings] Change Theme',
  CHANGE_AUTO_NIGHT_AUTO_MODE = '[Settings] Change Auto Night Mode',
  CHANGE_STICKY_HEADER = '[Settings] Change Sticky Header',
  CHANGE_ANIMATIONS_PAGE = '[Settings] Change Animations Page',
  CHANGE_ANIMATIONS_PAGE_DISABLED = '[Settings] Change Animations Page Disabled',
  CHANGE_ANIMATIONS_ELEMENTS = '[Settings] Change Animations Elements',
  CHANGE_HOUR = '[Settings] Change Hours',
  
  UPDATE = '[Settings] Update',
  UPDATE_SUCCESS = '[Settings] Update Success',
  UPDATE_ERROR = '[Settings] Update Error',  
}

export class ActionSettingsRetrieve implements Action {
  readonly type = SettingsActionTypes.RETRIEVE;
  constructor(readonly payload: { locID: number }) { }
}

export class ActionSettingsRetrieveSuccess implements Action {
  readonly type = SettingsActionTypes.RETRIEVE_SUCCESS;

  constructor(readonly payload: { settings: Setting[] }) { }
}

export class ActionSettingsRetrieveError implements Action {
  readonly type = SettingsActionTypes.RETRIEVE_ERROR;

  constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export class ActionSettingsChangeLanguage implements Action {
  readonly type = SettingsActionTypes.CHANGE_LANGUAGE;

  constructor(readonly payload: { language: Language }) { }
}

export class ActionSettingsChangeTheme implements Action {
  readonly type = SettingsActionTypes.CHANGE_THEME;

  constructor(readonly payload: { theme: string }) { }
}

export class ActionSettingsChangeAutoNightMode implements Action {
  readonly type = SettingsActionTypes.CHANGE_AUTO_NIGHT_AUTO_MODE;

  constructor(readonly payload: { autoNightMode: boolean }) { }
}

export class ActionSettingsChangeStickyHeader implements Action {
  readonly type = SettingsActionTypes.CHANGE_STICKY_HEADER;

  constructor(readonly payload: { stickyHeader: boolean }) { }
}

export class ActionSettingsChangeAnimationsPage implements Action {
  readonly type = SettingsActionTypes.CHANGE_ANIMATIONS_PAGE;

  constructor(readonly payload: { pageAnimations: boolean }) { }
}

export class ActionSettingsChangeAnimationsPageDisabled implements Action {
  readonly type = SettingsActionTypes.CHANGE_ANIMATIONS_PAGE_DISABLED;

  constructor(readonly payload: { pageAnimationsDisabled: boolean }) { }
}

export class ActionSettingsChangeAnimationsElements implements Action {
  readonly type = SettingsActionTypes.CHANGE_ANIMATIONS_ELEMENTS;

  constructor(readonly payload: { elementsAnimations: boolean }) { }
}

export class ActionSettingsChangeHour implements Action {
  readonly type = SettingsActionTypes.CHANGE_HOUR;

  constructor(readonly payload: { hour: number }) { }
}

export class ActionSettingsUpdate implements Action {
  readonly type = SettingsActionTypes.UPDATE;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { data: any , locID: number}) { }
}
export class ActionSettingsUpdateSuccess implements Action {
  readonly type = SettingsActionTypes.UPDATE_SUCCESS;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { data: BaseResponse }) { }
}

export class ActionSettingsUpdateError implements Action {
  readonly type = SettingsActionTypes.UPDATE_ERROR;

  //TODO: timestamp should be a date time. 
  constructor(readonly payload: { error?: HttpErrorResponse }) { }
}

export type SettingsActions =
  | ActionSettingsChangeLanguage
  | ActionSettingsChangeTheme
  | ActionSettingsChangeAnimationsPage
  | ActionSettingsChangeAnimationsPageDisabled
  | ActionSettingsChangeAnimationsElements
  | ActionSettingsChangeAutoNightMode
  | ActionSettingsChangeStickyHeader
  | ActionSettingsChangeHour
  | ActionSettingsRetrieve
  | ActionSettingsRetrieveSuccess
  | ActionSettingsRetrieveError
  | ActionSettingsUpdate
  | ActionSettingsUpdateSuccess
  | ActionSettingsUpdateError;

