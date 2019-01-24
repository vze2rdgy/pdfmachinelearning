import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PaymentsComponent } from './payments/payments.component';
import { HomeComponent } from './home/home.component';
import { UploadComponent } from './upload/upload.component';

const routes: Routes = [
  {
    path: '', component: PaymentsComponent,
    children: [
      { path: '', redirectTo: 'home', data: { title: 'lynx.payments.title' } },
      { path: 'home', component: HomeComponent, data: { title: 'lynx.payments.title' } },
      { path: 'upload', component: UploadComponent, data: { title: 'lynx.payments.menu.upload' } },      
    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PaymentsRoutingModule { }
