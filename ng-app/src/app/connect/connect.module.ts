import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ConnectRoutingModule } from './connect-routing.module';
import { ConnectComponent } from './connect/connect.component';
import { CKEditorModule } from 'ng2-ckeditor';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared';
import { ScheduleComponent } from './schedule/schedule.component';
import { TemplatesComponent } from './templates/templates.component';
import { StoreModule } from '@ngrx/store';
import { FEATURE_NAME, reducers } from './connect.state';
import { EffectsModule } from '@ngrx/effects';
import { TemplateEffects } from './templates/template.effects';
import { ConnectGuard } from './connect.gaurd';
import { ConnectResolver } from './connect.resolver';
import { SendmessageComponent } from './sendmessage/sendmessage.component';

@NgModule({
  declarations: [TemplatesComponent, ConnectComponent, ScheduleComponent, SendmessageComponent],
  imports: [CommonModule, ConnectRoutingModule, FormsModule, CKEditorModule, SharedModule,
    StoreModule.forFeature(FEATURE_NAME, reducers),
    EffectsModule.forFeature(
      [TemplateEffects]
    )
  ],
  providers: [ ConnectGuard, ConnectResolver ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class ConnectModule { }
