import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { AuthGuardService } from '@app/core';

const routes: Routes = [
  {
    path: '',
    component: RegisterComponent,
    data: { title: 'lynx.examples.menu.stocks' },
    canActivate: [AuthGuardService]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RegistrationRoutingModule { }
