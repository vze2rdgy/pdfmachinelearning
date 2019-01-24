import { AppState } from '@app/core';
import { Setting } from '@app/shared/models/setting';
import { HttpErrorResponse } from '@angular/common/http';
import { UpdateStatus } from '@app/shared/models/update-status';

export const NIGHT_MODE_THEME = 'BLACK-THEME';

export type Language = 'en' | 'sk' | 'de' | 'fr' | 'es' | 'pt-br';

export interface SettingsState {
  language: string;
  theme: string;
  autoNightMode: boolean;
  nightTheme: string;
  stickyHeader: boolean;
  pageAnimations: boolean;
  pageAnimationsDisabled: boolean;
  elementsAnimations: boolean;
  hour: number;
  locationdetails?: Setting[];
  lcoationretrieveerror? : HttpErrorResponse;
  updateStatus?: UpdateStatus;
}

export interface State extends AppState {
  settings: SettingsState;
}
