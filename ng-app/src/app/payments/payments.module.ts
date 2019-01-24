import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PaymentsRoutingModule } from './payments-routing.module';
import { PaymentsComponent } from './payments/payments.component';
import { HomeComponent } from './home/home.component';
import { UploadComponent } from './upload/upload.component';
import { SharedModule } from '@app/shared';
import { StoreModule } from '@ngrx/store';
import { FEATURE_NAME, reducers } from './payments.state';
import { EffectsModule } from '@ngrx/effects';
import { PaymentsEffects } from './payment.effects';

@NgModule({
  declarations: [PaymentsComponent, HomeComponent, UploadComponent],
  imports: [
    CommonModule,
    SharedModule,
    PaymentsRoutingModule,
    StoreModule.forFeature(FEATURE_NAME, reducers),
    EffectsModule.forFeature(
      [PaymentsEffects]
    ),
  ]
})
export class PaymentsModule {
  constructor(){}
 }
