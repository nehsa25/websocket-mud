import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RelatedContentComponent } from './related-content.component';

describe('RelatedContentComponent', () => {
  let component: RelatedContentComponent;
  let fixture: ComponentFixture<RelatedContentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RelatedContentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RelatedContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
