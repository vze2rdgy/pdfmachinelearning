import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StudentsRoutingModule } from './students-routing.module';
import { HomeComponent } from './home/home.component';
import { DetailsComponent } from './details/details.component';
import { UploadComponent } from './upload/upload.component';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { HttpClient } from '@angular/common/http';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { environment } from '@env/environment';
import { TuitionsComponent } from './tuitions/tuitions.component';
import { StoreModule } from '@ngrx/store';
import { FEATURE_NAME, reducers } from './student.state';
import { SharedModule } from '@app/shared';
import { EffectsModule } from '@ngrx/effects';
import { StudentsHomeEffects } from './home/home.effects';
import { StudentsComponent } from './students/students.component';
import { StudentsService } from './students.service';
import { SatPopoverModule } from '@ncstate/sat-popover';
import { EditForm } from './tuitions/edit-form.component';
import { TuitionsEffects } from './tuitions/tuitions.effects';
import { AppModule } from '@app/app.module';
import { PaymecodeGenDialogComponent } from './home/paymecode-gen-dialog/paymecode-gen-dialog.component';

@NgModule({
  
  imports: [
    // AppModule,
    CommonModule,
    SharedModule,
    StudentsRoutingModule,
    StoreModule.forFeature(FEATURE_NAME, reducers),
    EffectsModule.forFeature(
      [StudentsHomeEffects, TuitionsEffects]
    ),

    // TranslateModule.forChild({
    //   loader: {
    //     provide: TranslateLoader,
    //     useFactory: HttpLoaderFactory,
    //     deps: [HttpClient]
    //   },
    //   isolate: true
    // }), 
    SatPopoverModule,
  ],
  declarations: [HomeComponent, DetailsComponent, UploadComponent, TuitionsComponent, StudentsComponent, EditForm, PaymecodeGenDialogComponent],
  providers: [StudentsService],
  entryComponents:[PaymecodeGenDialogComponent]

})
export class StudentsModule { 
  constructor(){}
}

export function HttpLoaderFactory(http: HttpClient) {
  console.log("iam here");
  return new TranslateHttpLoader(
    http,
    `${environment.i18nPrefix}/assets/i18n/students/`,
    '.json'
  );
}