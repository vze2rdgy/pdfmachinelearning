import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConnectComponent } from './connect/connect.component';
import { TemplatesComponent } from './templates/templates.component';
import { ScheduleComponent } from './schedule/schedule.component';
import { ConnectGuard } from './connect.gaurd';
import { ConnectResolver } from './connect.resolver';
import { SendmessageComponent } from './sendmessage/sendmessage.component';

const routes: Routes = [
  {
    path: '',
    component: ConnectComponent,
    children: [
      { path: '', redirectTo: 'templates', data: { title: 'lynx.connect.templates.title' } },
      {
        path: 'templates',
        component: TemplatesComponent,        
        resolve: { templates: ConnectResolver },
        data: { title: 'lynx.connect.templates.title' }
      },
      {
        path: 'schedule',
        component: ScheduleComponent,
        data: { title: 'lynx.connect.schedule.title' }
      },
      {
        path: 'sendmessage',
        component: SendmessageComponent,
        data: { title: 'lynx.connect.sendmessage.title' }
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ConnectRoutingModule {}
