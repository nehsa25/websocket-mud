import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DupeNameComponent } from './dupe-name.component';

describe('DupeNameComponent', () => {
  let component: DupeNameComponent;
  let fixture: ComponentFixture<DupeNameComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DupeNameComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DupeNameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
