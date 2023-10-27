import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WordCloudContainerComponent } from './word-cloud-container/word-cloud-container.component';
import { TeamsDescComponent } from './teams-desc/teams-desc.component'

const routes: Routes = [
  { path: '', component: WordCloudContainerComponent },
  { path: 'team-description', component: TeamsDescComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
