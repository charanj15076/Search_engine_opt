import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WordCloudContainerComponent } from './word-cloud-container/word-cloud-container.component';
import { StatsContainerComponent } from './stats-container/stats-container.component';

const routes: Routes = [
  { path: '', component: WordCloudContainerComponent },
  { path: 'stats', component: StatsContainerComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
