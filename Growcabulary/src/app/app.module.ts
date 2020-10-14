import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA, APP_INITIALIZER } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { ChartsModule } from 'ng2-charts';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { WordListComponent } from './word-list/word-list.component';
import { WordItemComponent } from './word-item/word-item.component';
import { WordDetailComponent } from './word-detail/word-detail.component';
import { PriceDetailComponent } from './price-detail/price-detail.component';
import { AboutComponent } from './about/about.component';
import { WordListService } from './word-list.service';
import { LineChartComponent } from './line-chart/line-chart.component';
import { WordSearchComponent } from './word-search/word-search.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    WordListComponent,
    WordItemComponent,
    WordDetailComponent,
    PriceDetailComponent,
    AboutComponent,
    LineChartComponent,
    WordSearchComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ChartsModule,
    FormsModule,
    MDBBootstrapModule.forRoot()
  ],
  schemas: [NO_ERRORS_SCHEMA],
  providers: [WordListService,
    {
      provide: APP_INITIALIZER,
      useFactory: (wordListService: WordListService) => () => { return wordListService.load() },
      deps: [WordListService],
      multi: true
    }],
  bootstrap: [AppComponent]
})
export class AppModule { }
