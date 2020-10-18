import { Word } from './../word.model';
import { Component, OnInit, OnDestroy, ViewChildren, QueryList, ElementRef, ViewContainerRef } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Subscription } from 'rxjs';
import { WordListService } from '../word-list.service';
import { WordItemComponent } from '../word-item/word-item.component';

@Component({
  selector: 'app-word-list',
  templateUrl: './word-list.component.html',
  styleUrls: ['./word-list.component.scss']
})
export class WordListComponent implements OnDestroy {
  idx: number;
  readMode: boolean = true;
  subscriptionParams: Subscription; subscriptionQueryParams: Subscription; 
  wordList: Word[];
  @ViewChildren('wordItem') wordItems: QueryList<ElementRef>;
  
  constructor(private activatedRoute: ActivatedRoute, public wordListService: WordListService) {
    this.idx = 0;
    this.wordList = [];
    this.getRouteParams();
  }

  ngOnInit() {}
  
  ngAfterViewInit() {
    this.getRouteQueryParams();
  }
  
  ngAfterViewChecked() {
    if (this.readMode) {
      let items = this.wordItems.toArray();
      items[this.idx].nativeElement.scrollIntoView();
    }
  }
  
  ngOnDestroy() {
    this.subscriptionParams.unsubscribe();
    this.subscriptionQueryParams.unsubscribe();
  }
  
  getRouteParams() {
    this.subscriptionParams = this.activatedRoute.params.subscribe(params => {
      this.wordList = this.wordListService.getWordList(params.folder);
    });
  }
  
  getRouteQueryParams() {
    this.subscriptionQueryParams = this.activatedRoute.queryParams.subscribe(queryParams => {
      if (!this.readMode || !queryParams.hasOwnProperty('index'))
        return;
      let index = Number(queryParams.index), items = this.wordItems.toArray();
      if (!isNaN(index) && index >= 0 && index < items.length)
        this.idx = index;
    });
  }
  
  toggleMode() {
    this.readMode = !this.readMode;
  }
  
  cardClick(index: number) {
    this.idx = index;
    this.toggleMode();
  }
}