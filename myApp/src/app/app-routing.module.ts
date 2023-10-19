import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WordCloudContainerComponent } from './word-cloud-container/word-cloud-container.component';
import { StatsContainerComponent } from './stats-container/stats-container.component';
import { TeamsDescComponent } from './teams-desc/teams-desc.component';
import { GuideComponent } from './guide/guide.component';
import { AlgorithmsComponent } from './algorithms/algorithms.component';

const routes: Routes = [
  { path: '', component: WordCloudContainerComponent },
  { path: 'stats', component: StatsContainerComponent },
  { path: 'team-description', component: TeamsDescComponent},
  { path: 'guide', component: GuideComponent},
  { path: 'algorithms', component: AlgorithmsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
