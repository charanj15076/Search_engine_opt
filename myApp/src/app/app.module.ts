import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { BodyComponent } from './body/body.component';
import { StatsContainerComponent } from './stats-container/stats-container.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { WordCloudContainerComponent } from './word-cloud-container/word-cloud-container.component';
import { TeamsDescComponent } from './teams-desc/teams-desc.component';
import { GuideComponent } from './guide/guide.component';
import { AlgorithmsComponent } from './algorithms/algorithms.component';
import { HighchartsChartModule } from 'highcharts-angular';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    BodyComponent,
    StatsContainerComponent,
    WordCloudContainerComponent,
    TeamsDescComponent,
    GuideComponent,
    AlgorithmsComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule, ReactiveFormsModule, HighchartsChartModule, BrowserAnimationsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
