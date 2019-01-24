import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component'
import { UploadComponent } from './upload/upload.component';
import { TuitionsComponent } from './tuitions/tuitions.component'
import { DetailsComponent } from './details/details.component';
import { StudentsComponent } from './students/students.component';

const routes: Routes = [
  {
    path: '', component: StudentsComponent,
    children: [
      { path: '', redirectTo: 'home', data: { title: 'lynx.students.title' } },
      { path: 'home', component: HomeComponent, data: { title: 'lynx.students.title' } },
      { path: 'upload', component: UploadComponent, data: { title: 'lynx.students.menu.upload' } },
      { path: 'tuitions', component: TuitionsComponent, data: { title: 'lynx.students.menu.tuitions' } },
      
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StudentsRoutingModule { }
