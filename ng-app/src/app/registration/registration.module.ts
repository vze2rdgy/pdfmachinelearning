import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RegistrationRoutingModule } from './registration-routing.module';
import { RegisterComponent } from './register/register.component';
import { SharedModule } from '@app/shared';
import { StoreModule } from '@ngrx/store';
import { FEATURE_NAME } from './registration.state';
import { registrationReducer } from './registration.reducer';
import { EffectsModule } from '@ngrx/effects';
import { RegistrationEffects } from './registration.effects';

@NgModule({
  declarations: [RegisterComponent],
  imports: [
    CommonModule,
    SharedModule,
    RegistrationRoutingModule,
    StoreModule.forFeature(FEATURE_NAME, registrationReducer),
    EffectsModule.forFeature(
      [RegistrationEffects]
    ),
  ]
})
export class RegistrationModule {
  constructor() { }
}

