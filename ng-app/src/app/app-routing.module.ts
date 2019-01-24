import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SettingsContainerComponent } from './settings';
import { AuthHandlerComponent } from './shared/auth-handler/auth-handler.component';
import { AuthGuardService } from './core';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'about',
    pathMatch: 'full'
  },
  {
    path: 'settings',
    component: SettingsContainerComponent,
    data: { title: 'lynx.menu.settings' }
  },
  {
    path: 'examples',
    loadChildren: 'app/examples/examples.module#ExamplesModule'
  },
  {
    path: 'authhandler',
    component: AuthHandlerComponent,
    data: { title: 'lynx.menu.settings' }
  },
  {
    path: 'register',
    loadChildren: 'app/registration/registration.module#RegistrationModule'
  },
  {
    path: 'students',
    loadChildren: 'app/students/students.module#StudentsModule'
    // canActivate: [AuthGuardService]
  },
  {
    path: 'connect',
    loadChildren: 'app/connect/connect.module#ConnectModule'
    // canActivate: [AuthGuardService]
  },
  {
    path: 'payments',
    loadChildren: 'app/payments/payments.module#PaymentsModule'
    // canActivate: [AuthGuardService]
  },
  {
    path: '**',
    redirectTo: 'about'
  }
];

@NgModule({
  // useHash supports github.io demo page, remove in your app
  imports: [
    RouterModule.forRoot(routes, {
      useHash: true,
      scrollPositionRestoration: 'enabled'
    })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
